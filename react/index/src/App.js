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

const Slider = (props) => {
  return (
    <div className="slidecontainer">
      <label for={`${props.id}`}>{props.label}</label>
      <input type="range" min={props.min} max={props.max} className={props.className} id={props.id}></input>
    </div>
  )
}

const Brgb = () => {
  return (
    <div>
      <Slider min="10" max="1000" className="slider-br" id="brightness" label="Brightness:"/>
      <Slider min="10" max="1000" className="slider-r" id="R" label="RED:"/>
      <Slider min="10" max="1000" className="slider-g" id="G" label="GREEN:"/>
      <Slider min="10" max="1000" className="slider-b" id="B" label="BLUE:"/>
    </div>
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
      <Brgb/>
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
