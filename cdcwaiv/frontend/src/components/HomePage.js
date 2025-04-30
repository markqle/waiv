import React, { Component } from "react";
import Profile from "./Profile";
import Student from "./Student";
import MonthlyListing from "./MonthlyListing";
import Employee from "./Employee";
import Login from './Login';
import Counseling from "./Counseling";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Link,
  Redirect,
} from "react-router-dom";

export default class HomePage extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (<Router>
        <Routes>
            <Route path="/" element={<p>This is the home page</p>} />
            <Route path='/profile' element = {<Profile/>}/>
            <Route path='/employee' element = {<Employee/>}/>
            <Route path='/student' element = {<Student/>}/>
            <Route path='/monthly-listing' element = {<MonthlyListing/>}/>
            <Route path='/login' element = {<Login/>}/>
            <Route path='/counseling' element = {<Counseling/>}/>
        </Routes>
    </Router>);
  }
}
