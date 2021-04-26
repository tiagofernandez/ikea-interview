import logo from "./logo.png";
import "./App.css";
import { Button } from "@material-ui/core";

function App() {
    return (
        <div className="App">
            <header className="App-header">
                <img src={logo} className="App-logo" alt="logo" />
                <Button color="primary">Search</Button>
            </header>
        </div>
    );
}

export default App;
