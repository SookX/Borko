import React, { useState } from 'react';
import '../style/home.css'
import homeImage from '../dist/img/home.png'
import styled from 'styled-components';
import Spline from '@splinetool/react-spline';
import Nav from './Nav';

const Button = () => {
    return (
      <StyledWrapper>
        <button>
          Get Started
        </button>
      </StyledWrapper>
    );
  }

const StyledWrapper = styled.div`
  button {
    position: relative;
    padding: 10px 20px;
    border-radius: 7px;
    border: 1px solid rgb(61, 106, 255);
    font-size: 14px;
    text-transform: uppercase;
    font-weight: 600;
    letter-spacing: 2px;
    background: transparent;
    color: #fff;
    overflow: hidden;
    box-shadow: 0 0 0 0 transparent;
    -webkit-transition: all 0.2s ease-in;
    -moz-transition: all 0.2s ease-in;
    transition: all 0.2s ease-in;
  }

  button:hover {
    background: rgb(61, 106, 255);
    box-shadow: 0 0 30px 5px rgba(0, 142, 236, 0.815);
    -webkit-transition: all 0.2s ease-out;
    -moz-transition: all 0.2s ease-out;
    transition: all 0.2s ease-out;
  }

  button:hover::before {
    -webkit-animation: sh02 0.5s 0s linear;
    -moz-animation: sh02 0.5s 0s linear;
    animation: sh02 0.5s 0s linear;
  }

  button::before {
    content: '';
    display: block;
    width: 0px;
    height: 86%;
    position: absolute;
    top: 7%;
    left: 0%;
    opacity: 0;
    background: #fff;
    box-shadow: 0 0 50px 30px #fff;
    -webkit-transform: skewX(-20deg);
    -moz-transform: skewX(-20deg);
    -ms-transform: skewX(-20deg);
    -o-transform: skewX(-20deg);
    transform: skewX(-20deg);
  }

  @keyframes sh02 {
    from {
      opacity: 0;
      left: 0%;
    }

    50% {
      opacity: 1;
    }

    to {
      opacity: 0;
      left: 100%;
    }
  }

  button:active {
    box-shadow: 0 0 0 0 transparent;
    -webkit-transition: box-shadow 0.2s ease-in;
    -moz-transition: box-shadow 0.2s ease-in;
    transition: box-shadow 0.2s ease-in;
  }`;

const Home = () => {

  
    return (
      <div>
        <Nav/>
        <div className='home'>
            <div className='left'>
                <div className='text'>
                    <h1>Welcome to Borko – Bulgaria's First Voice Assistant</h1>
                    <p>Discover a new way to simplify your life with Borko, the voice assistant designed to understand you, assist you, and make everyday tasks effortless.</p>
                    <br />
                    <a href='/login'>
                    <Button/>
                    </a>
                    
                </div>
                
                
            </div>
            <div className='right'>
            <Spline
        scene="https://prod.spline.design/SLRIDw8tokmtlfqm/scene.splinecode" 
      />
            </div>
        </div>
        </div>
    );
  };
  


export default Home;