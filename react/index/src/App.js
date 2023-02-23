import logo from './logo.svg';
import './App.css';

//const url = (new URL(document.location)).origin
const url = 'http://localhost:3001'

const Header = () => {
  return (
    <div className="header">
      <a className="button" href="/">Control Panel</a>
      <a className="button" href="/settings">Settings</a>
      <a className="button" href="/alarm">Alarm</a>
    </div>
  )
}

const Button = (props) => {
  return (
    <input type="button" className="button" onClick={props.onClick} value={props.value}/>
  )
}

const MainControls = () => {

  const toggleLights = () => {
    console.log('Toggled lights')
    fetch(`${url}/lightState?toggle=change`)
      .then(res => res.json())
      .then(res => console.log(res))
  }

  return (
    <div className="content">
      <div className="Content-box">
        <p className="Main-Text">RGB LED strip control panel</p>
      </div>
      <Button onClick={toggleLights} value="Toggle Lights"/>
    </div>
  )
}

const App = () => {
  return (
    <div className="App">
      <Header/>
      <MainControls/>
    </div>
  );
}

export default App;
