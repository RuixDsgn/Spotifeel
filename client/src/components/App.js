import React, { useEffect, useState } from "react";
import { Switch, Route } from "react-router-dom";
import LandingPage from "./LandingPage";
import Question1 from "./Question1";
import Question2 from "./Question2";
import ConnectSpotify from "./ConnectSpotify";

function App() {
  return 
  <div>
    <LandingPage />
    <Question1 />
    <Question2 />
    <ConnectSpotify />
  </div>


}

export default App;
