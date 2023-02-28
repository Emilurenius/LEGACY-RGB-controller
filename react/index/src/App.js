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
      <input type="range" min={props.min} max={props.max} className={props.className} id={props.id} onChange={props.onChange}></input>
    </div>
  )
}

const Brgb = (props) => {
  return (
    <div>
      <Slider min="10" max="1000" className="slider-br" id="br" label="Brightness:" onChange={props.onChange}/>
      <Slider min="10" max="1000" className="slider-r"  id="r"  label="RED:"        onChange={props.onChange}/>
      <Slider min="10" max="1000" className="slider-g"  id="g"  label="GREEN:"      onChange={props.onChange}/>
      <Slider min="10" max="1000" className="slider-b"  id="b"  label="BLUE:"       onChange={props.onChange}/>
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

  const brgbSlidersListener = (e) => {
    console.log(e.target.id)
    console.log(e.target.value)
    fetch(`${url}/rgb?${e.target.id}=${e.target.value}`)
  }

  return (
    <div className="content">
      <div className="Content-box">
        <p className="Main-Text">RGB LED strip control panel</p>
      </div>
      <Button onClick={toggleLights} value="Toggle Lights"/>
      <Brgb onChange={brgbSlidersListener}/>
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
