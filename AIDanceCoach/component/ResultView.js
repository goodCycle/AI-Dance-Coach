import React, { Component } from 'react';
import PropTypes from 'prop-types';
import {
  StyleSheet,
  View,
  Text,
  TouchableOpacity,
} from 'react-native';
import Video from 'react-native-video';
import CameraRoll from '@react-native-community/cameraroll';

const RNFS = require('react-native-fs');
const video = require('./sample.mp4');

const styles = StyleSheet.create({
  container: {
    flex: 1,
    flexDirection: 'column',
  },
  preview: {
    flex: 1,
    backgroundColor: 'red',
  },
  buttonContainer: {
    flex: 0.2,
    flexDirection: 'column',
    justifyContent: 'center',
    backgroundColor: '#B82303',
  },
  button: {
    backgroundColor: '#fff',
    borderRadius: 5,
    padding: 10,
    marginHorizontal: 70,
    alignItems: 'center',
    justifyContent: 'center',
  },
  buttonText: {
    fontSize: 14,
    color: '#B82303',
    fontWeight: 'bold',
  },
});

class ResultView extends Component {
  constructor(props) {
    super(props);
    this.state = this.getInitialState();
  }

  getInitialState() {
    return {
    };
  }

  saveVideoToCameraRoll = async (uri) => {
    let videoUri = null;
    try {
      videoUri = await CameraRoll.saveToCameraRoll(uri);
      console.log('saved!', videoUri);
    } catch (error) {
      console.log(error.message);
    }
    return videoUri;
  }

  render() {
    const { resultVideoPath, flushOpenPoseResult } = this.props;
    const sampleVideoUri = `${resultVideoPath}/media/temp_vid/sample.mp4`;
    const trialVideoUri = `${resultVideoPath}/media/temp_vid/trial.mp4`;

    RNFS.exists(sampleVideoUri).then((exist) => { console.log('file', exist); });
    console.log('sampleVideoUri', sampleVideoUri);

    return (
      <View style={styles.container}>
        <View style={styles.preview}>
          <View style={{flex: 1}}>
            <Video source={{ uri: sampleVideoUri }} // Can be a URL or a local file.
              // ref={(ref) => {
              //   this.player = ref
              // }}                                      // Store reference
              // onBuffer={this.onBuffer}
              onLoadStart={(props) => console.log(props)}
              onLoad={(props) => console.log(props)}             // Callback when remote video is buffering
              onError={(error) => console.error(error)}               // Callback when video cannot be loaded
              style={
                {
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  bottom: 0,
                  right: 0,
                }
              }
              repeat
            />
          </View>
          <View style={{flex: 1}}>
          <Video source={{ uri: trialVideoUri }} // Can be a URL or a local file.
            // ref={(ref) => {
            //   this.player = ref
            // }}                                      // Store reference
            // onBuffer={this.onBuffer}
            onLoadStart={(props) => console.log(props)}
            onLoad={(props) => console.log('tiral', props)}             // Callback when remote video is buffering
            onError={(error) => console.error(error)}               // Callback when video cannot be loaded
            style={
              {
                position: 'absolute',
                top: 0,
                left: 0,
                bottom: 0,
                right: 0,
              }
            }
            repeat
          />
          </View>
        </View>
        <View style={styles.buttonContainer}>
          <TouchableOpacity
            onPress={flushOpenPoseResult}
            style={styles.button}
          >
            <Text style={styles.buttonText}>
              Back To Record
            </Text>
          </TouchableOpacity>
        </View>
      </View>
    );
  }
}

ResultView.propTypes = {
  resultVideoPath: PropTypes.string.isRequired,
  flushOpenPoseResult: PropTypes.func.isRequired,
};

export default ResultView;
