/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 *
 * @format
 * @flow
 */

import React from 'react';
import MainView from './component/MainView';
import CameraView from './component/CameraView';

export class App extends React.Component {
  state = {
    recording: false
  }

  onPressStartRecord = () => {
    if (!this.state.recording) {
      this.setState({ recording: true });
    }
  }

  onPressStopRecord = () => {
    if (this.state.recording) {
      this.setState({ recording: false });
    }
  }

  render() {
    return (
      this.state.recording
      ? <CameraView onPressStopRecord={this.onPressStopRecord}/>
      : <MainView onPressStartRecord={this.onPressStartRecord}/>
    );
  }
};

export default App;
