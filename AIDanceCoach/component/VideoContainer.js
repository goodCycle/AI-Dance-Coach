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
      hasOpenPoseResult: false,
      openPoseResult: null,
    };
  }

  setOpenPoseResult = (result) => {
    this.setState({
      hasOpenPoseResult: true,
      openPoseResult: result,
    });
  }

  flushOpenPoseResult = () => {
    this.setState({
      hasOpenPoseResult: false,
      openPoseResult: null,
    });
  }

  render() {
    const { onPressStopRecord } = this.props;
    const { hasOpenPoseResult, openPoseResult } = this.state;

    return (
      <View style={styles.container}>
        <HeaderComponent
          leftIcon="chevron-left"
          onPressLeftIcon={onPressStopRecord}
          headerText="Record Dance"
        />
        {
          hasOpenPoseResult
            ? (
              <ResultView
                openPoseResult={openPoseResult}
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
