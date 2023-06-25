import React from "react";
import { useHistory } from "react-router-dom";
import { Navbar, Nav, Container, NavDropdown } from "react-bootstrap";
import logo from "../Resources/images/logo.png";

const NavBar = () => {
  let history = useHistory();
  const redirect = () => {
    history.push("/feedback");
  };
  const email = "davidtest@gmail.com";
  const userID = "Powerbooster19823";

  return (
    <Navbar bg="secondary" variant="dark" className="ml-auto">
      <Container>
        <Navbar.Brand href="/">
          <img
            alt=""
            src={logo}
            width="30"
            height="32"
            className="d-inline-block align-top"
          />{" "}
          The Fruit Shop
        </Navbar.Brand>
        <Navbar.Toggle />
        <Navbar.Collapse>
          {/** 
          <Nav
            className="justify-content-end"
            style={{ width: "95%", color: "white" }}
          >
            {email}
          </Nav>
          */}
        </Navbar.Collapse>
        <Nav className="me-auto">
          <NavDropdown title={email} id="collasible-nav-dropdown">
            <NavDropdown.Item href="#userID">{userID}</NavDropdown.Item>

            <NavDropdown.Divider />
            <NavDropdown.Item href="#action/3.2">
              User Settings
            </NavDropdown.Item>
            <NavDropdown.Item href="#action/3.4">About</NavDropdown.Item>
          </NavDropdown>
        </Nav>
        {/** <button class="btn btn-outline-success" onClick={redirect}>
          Submit Feedback
  </button> */}
      </Container>
    </Navbar>
  );
};

export default NavBar;
