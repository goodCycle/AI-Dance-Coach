import React from 'react';
import MainContainer from './component/MainContainer';
import VideoContainer from './component/VideoContainer';

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
        ? <VideoContainer onPressStopRecord={this.onPressStopRecord} />
        : <MainContainer onPressStartRecord={this.onPressStartRecord} />
    );
  }
}

export default App;
