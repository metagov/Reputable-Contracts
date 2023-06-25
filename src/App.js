import "./App.css";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import Feedback from "./Pages/Feedback";
import Shop from "./Pages/Shop";
import NavBar from "./Pages/NavBar";
import UserFreshFeedback from "./Pages/UserFreshFeedback";
import { CartProvider } from "react-use-cart";
import Cart from "./Pages/Cart";
import Dashboard from "./Pages/Dashboard";
import FirebaseData from "./Pages/FirebaseData";

function App() {
  return (
    <Router>
      <NavBar />
      <Switch>
        <Route path="/" exact>
          <CartProvider>
            <Shop />
            <Cart />
          </CartProvider>
        </Route>
        <Route path="/dashboard" exact>
          <Dashboard />
        </Route>
        <Route path="/firebase" exact>
          <FirebaseData />
        </Route>
        <Route path="/feedback" exact>
          <UserFreshFeedback />
        </Route>
        <Route path="/feedback/:userID/:sellerID/:tokenID/:campaignID/" exact>
          <Feedback />
        </Route>
      </Switch>
    </Router>
  );
}

export default App;
