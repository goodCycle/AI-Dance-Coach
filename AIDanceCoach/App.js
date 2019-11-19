import React from 'react';
import MainView from './component/MainView';
import CameraView from './component/CameraView';

class App extends React.Component {
  constructor() {
    super();
    this.state = {
      recording: false,
    };
  }

  onPressStartRecord = () => {
    const { recording } = this.state;
    if (!recording) {
      this.setState({ recording: true });
    }
  }

  onPressStopRecord = () => {
    const { recording } = this.state;
    if (recording) {
      this.setState({ recording: false });
    }
  }

  render() {
    const { recording } = this.state;

    return (
      recording
        ? <CameraView onPressStopRecord={this.onPressStopRecord} />
        : <MainView onPressStartRecord={this.onPressStartRecord} />
    );
  }
}

export default App;
