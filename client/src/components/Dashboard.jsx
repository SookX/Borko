import React, { useEffect, useRef, useState } from 'react';
import styled from 'styled-components';
import toWav from 'audiobuffer-to-wav';
import Spline from '@splinetool/react-spline';
import 'axios'
import '../style/dashboard.css';
import axios from 'axios';

const AudioSender = () => {
  const ws = useRef(null);
  const mediaRecorder = useRef(null);
  const audioContext = useRef(new (window.AudioContext || window.webkitAudioContext)());
  const analyser = useRef(null);
  const recordedChunks = useRef([]);
  const [status, setStatus] = useState("Натисни кръгчето, за да зпочнеш");  // to hold status
  const silenceTimeout = useRef(null);
  const [isRecording, setIsRecording] = useState(false);
  const isRecordingRef = useRef(false); 
  const [volume, setVolume] = useState(0);

  // Effect to handle WebSocket connection
  useEffect(() => {
    const connectWebSocket = async () => {
      ws.current = new WebSocket('ws://localhost:8000/ws/audio/');
      ws.current.onopen = () => console.log('WebSocket connected');
      ws.current.onmessage = async (event) => {
        try {
          const response = JSON.parse(event.data);
          if (response.transcript) {
            setStatus(""); // reset status on new transcript
            const audioData = `data:audio/wav;base64,${response.transcript.audio}`;
            let audio = new Audio(audioData);
            audio.onended = () => {
              setStatus("Натисни кръгчето, за да зпочнеш");
            };
        
            // Play the audio
            await audio.play();
          }
        } catch (error) {
          console.error("Error parsing WebSocket message:", error);
        }
      };

      ws.current.onerror = (error) => console.error('WebSocket error:', error);
      ws.current.onclose = () => console.log('WebSocket disconnected');
    };

    connectWebSocket();

    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, []);  // Empty dependency array to run only on mount/unmount

  // Function to start recording
  const startRecording = async () => {
    setStatus("Борко те слуша...");
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const sourceNode = audioContext.current.createMediaStreamSource(stream);

      analyser.current = audioContext.current.createAnalyser();
      analyser.current.fftSize = 256;
      sourceNode.connect(analyser.current);

      const bufferLength = analyser.current.frequencyBinCount;
      const dataArray = new Uint8Array(bufferLength);

      const updateVolume = () => {
        analyser.current.getByteFrequencyData(dataArray);
        const avgVolume = dataArray.reduce((a, b) => a + b, 0) / bufferLength;
        setVolume(avgVolume);

        if (avgVolume < 10) {
          if (!silenceTimeout.current) {
            silenceTimeout.current = setTimeout(() => {
              if (isRecordingRef.current) {
                stopRecording();
              }
            }, 2000);
          }
        } else {
          if (silenceTimeout.current) {
            clearTimeout(silenceTimeout.current);
            silenceTimeout.current = null;
          }
        }

        requestAnimationFrame(updateVolume);
      };

      mediaRecorder.current = new MediaRecorder(stream);

      mediaRecorder.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          recordedChunks.current.push(event.data);
        }
      };

      mediaRecorder.current.onstop = async () => {
        const blob = new Blob(recordedChunks.current, { type: 'audio/webm' });
        recordedChunks.current = [];
        await processAudioChunk(blob);
      };

      mediaRecorder.current.start();
      setIsRecording(true);
      isRecordingRef.current = true; 
      updateVolume();
    } catch (error) {
      console.error("Error accessing microphone:", error);
    }
  };

  // Function to stop recording
  const stopRecording = () => {
    if (mediaRecorder.current && isRecordingRef.current) {
      mediaRecorder.current.stop();
      setIsRecording(false);
      isRecordingRef.current = false; 

      if (silenceTimeout.current) {
        clearTimeout(silenceTimeout.current);
        silenceTimeout.current = null;
      }
    }
  };

  // Process the audio chunk
  const processAudioChunk = async (blob) => {
    setStatus("Борко мисли...");
    const arrayBuffer = await blob.arrayBuffer();
    const audioBuffer = await audioContext.current.decodeAudioData(arrayBuffer);
    const wavBuffer = toWav(audioBuffer);
    const wavBlob = new Blob([wavBuffer], { type: 'audio/wav' });

    if (ws.current.readyState === WebSocket.OPEN) {
      ws.current.send(wavBlob);
      console.log("Sent WAV chunk:", wavBlob.size, "bytes");
    }
  };

  // Button component to handle the recording button
  const Button = () => {
    return (
        <button onClick={startRecording} disabled={isRecording}>
          <svg height={24} width={24} viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path d="M0 0h24v24H0z" fill="none" />
            <path d="M5 13c0-5.088 2.903-9.436 7-11.182C16.097 3.564 19 7.912 19 13c0 .823-.076 1.626-.22 2.403l1.94 1.832a.5.5 0 0 1 .095.603l-2.495 4.575a.5.5 0 0 1-.793.114l-2.234-2.234a1 1 0 0 0-.707-.293H9.414a1 1 0 0 0-.707.293l-2.234 2.234a.5.5 0 0 1-.793-.114l-2.495-4.575a.5.5 0 0 1 .095-.603l1.94-1.832C5.077 14.626 5 13.823 5 13zm1.476 6.696l.817-.817A3 3 0 0 1 9.414 18h5.172a3 3 0 0 1 2.121.879l.817.817.982-1.8-1.1-1.04a2 2 0 0 1-.593-1.82c.124-.664.187-1.345.187-2.036 0-3.87-1.995-7.3-5-8.96C8.995 5.7 7 9.13 7 13c0 .691.063 1.372.187 2.037a2 2 0 0 1-.593 1.82l-1.1 1.039.982 1.8zM12 13a2 2 0 1 1 0-4 2 2 0 0 1 0 4z" fill="currentColor" />
          </svg>
        </button>
    );
  };

  return (
    <div className="main">
      <div className="status-display">
        <p>{status}</p>  
      </div>
      <div className="blob">
        <Spline scene="https://prod.spline.design/tBczwsyOuZBxVhYS/scene.splinecode" onClick={startRecording} />
      </div>
    </div>
  );
};

export default AudioSender;
