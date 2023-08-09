import React from 'react';
import styled, { keyframes } from 'styled-components';

// Keyframes for the horizontal animation
const horizontalAnimation = keyframes`
  0% {
    transform: translateX(0);
  }
  100% {
    transform: translateX(-100%);
  }
`;

// Styled container for the rotating circle
const CircleContainer = styled.div`
  display: inline-block;
  position: relative;
  white-space: nowrap;
  overflow: hidden;
  animation: ${horizontalAnimation} 10s linear infinite;
`;

// Styled H1 element
const StyledH1 = styled.h1`
  font-size: 80px;
  font-weight: bold;
  margin: 0;
  display: inline-block;
`;

// Styled dot divider
const DotDivider = styled.span`
  font-size: 24px;
  margin: 20px 10px;
  color: white;
`;

const RotatingCircle = () => {
  return (
    <CircleContainer>
      <StyledH1>Spotifeel</StyledH1>
      <DotDivider>&#8226;</DotDivider>
      <StyledH1>Spotifeel</StyledH1>
      <DotDivider>&#8226;</DotDivider>
      <StyledH1>Spotifeel</StyledH1>
      <DotDivider>&#8226;</DotDivider>
      <StyledH1>Spotifeel</StyledH1>
      <DotDivider>&#8226;</DotDivider>
      <StyledH1>Spotifeel</StyledH1>
    </CircleContainer>
  );
};

export default RotatingCircle;


