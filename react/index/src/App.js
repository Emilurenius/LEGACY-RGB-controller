import logo from './logo.svg';
import './App.css';

const Header = () => {
  return (
    <div className="header">
      <a className="button" href="/">Control Panel</a>
      <a className="button" href="/settings">Settings</a>
      <a className="button" href="/alarm">Alarm</a>
    </div>
  )
}

const Button = (onClick, value) => {
  return (
    <input type="button" className="button" onClick="${onClick}"/>
  )
}

const MainControls = () => {
  return (
    <div className="content">
      <div class="Content-box">
        <p class="Main-Text">RGB LED strip control panel</p>
      </div>
    </div>
  )
}

function App() {
  return (
    <div className="App">
      <Header/>
      <MainControls/>
    </div>
  );
}

export default App;
