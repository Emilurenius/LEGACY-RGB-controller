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

const Button = (props) => {
  return (
    <input type="button" className="button" onClick={props.onClick} value={props.value}/>
  )
}

const MainControls = () => {

  const toggleLights = () => {
    console.log('Toggled lights')
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

function App() {
  return (
    <div className="App">
      <Header/>
      <MainControls/>
    </div>
  );
}

export default App;
