import React from 'react';
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import Home from './components/home/HGHome'

export default class App extends React.Component {
  render() {
    return(
      <Router>
      <div>
        <Route path="/" exact component={Home} />
      </div>
    </Router>   
    );
  }
}
