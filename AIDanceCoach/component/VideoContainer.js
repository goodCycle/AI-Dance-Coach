import React, { Component } from 'react';
import PropTypes from 'prop-types';
import {
  StyleSheet,
  View,
} from 'react-native';

import HeaderComponent from './HeaderComponent';
import CameraView from './CameraView';
import ResultView from './ResultView';

const styles = StyleSheet.create({
  container: {
    flex: 1,
    flexDirection: 'column',
  },
});

class VideoContainer extends Component {
  constructor(props) {
    super(props);
    this.state = this.getInitialState();
  }

  getInitialState() {
    return {
      recording: false,
      processing: false,
      resultVideoPath: null, // 'http://clips.vorwaerts-gmbh.de/big_buck_bunny.mp4',
    };
  }

  setOpenPoseResult = (path) => {
    this.setState({
      resultVideoPath: path,
    });
  }

  flushOpenPoseResult = () => {
    this.setState({
      resultVideoPath: null,
    });
  }

  render() {
    const { onPressStopRecord } = this.props;
    const { resultVideoPath } = this.state;

    return (
      <View style={styles.container}>
        <HeaderComponent
          leftIcon="chevron-left"
          onPressLeftIcon={onPressStopRecord}
          headerText="Record Dance"
        />
        {
          (resultVideoPath != null)
            ? (
              <ResultView
                resultVideoPath={resultVideoPath}
                flushOpenPoseResult={this.flushOpenPoseResult}
              />
            )
            : <CameraView setOpenPoseResult={this.setOpenPoseResult} />
        }
      </View>
    );
  }
}

VideoContainer.propTypes = {
  onPressStopRecord: PropTypes.func.isRequired,
};

export default VideoContainer;
