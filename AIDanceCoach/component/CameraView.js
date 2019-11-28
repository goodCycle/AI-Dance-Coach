import React, { Component } from 'react';
import PropTypes from 'prop-types';
import {
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
  ActivityIndicator,
} from 'react-native';

import { RNCamera } from 'react-native-camera';
import CameraRoll from '@react-native-community/cameraroll';
import ImagePicker from 'react-native-image-picker';
import Config from 'react-native-config';

const RNFS = require('react-native-fs');

const styles = StyleSheet.create({
  container: {
    flex: 1,
    flexDirection: 'column',
  },
  preview: {
    flex: 1,
    justifyContent: 'flex-end',
    alignItems: 'center',
  },
  recordButtonContainer: {
    flex: 0.2,
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#B82303',
  },
  recordButton: {
    backgroundColor: '#fff',
    borderRadius: 5,
    padding: 10,
    marginHorizontal: 70,
    alignItems: 'center',
    justifyContent: 'center',
  },
  recordButtonText: {
    fontSize: 14,
    color: '#B82303',
    fontWeight: 'bold',
  },
  horizontalButtonContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
});

class CameraView extends Component {
  constructor(props) {
    super(props);
    this.state = this.getInitialState();
  }

  getInitialState() {
    return {
      recording: false,
      hasOpenPoseResult: false,
      openPoseResult: null,
      recordedVideoUri: null,
      recordedVideoCodec: null,
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

  selectVideo = () => {
    const options = {
      mediaType:'video',
    };
    
    ImagePicker.launchImageLibrary(options, (response) => {
      // Same code as in above section!
      const source = { uri: response.uri, video: response.data };
      this.sendVideoAndConfigToServer(source.uri);
    });
  }

  sendVideoAndConfigToServer = async (uri) => {
    const data = new FormData();

    // Append mp4 video
    const codec = 'H264';
    const type = `video/${codec}`;
    data.append('file', {
      name: 'video.mp4',
      type,
      uri,
    });

    // Append json config
    const config = {
      is_sample: false,
      compare_to: 'sample_video_snipped.mp4',
    };
    const configJson = JSON.stringify(config);
    const jsonPath = RNFS.DocumentDirectoryPath + '/config.json';

    // Write json to the file
    await RNFS.writeFile(jsonPath, configJson, 'utf8');

    data.append('file', {
      name: 'video_config.json',
      type: 'applpication/json',
      uri: jsonPath,
    });

    try {
      const response = await fetch(Config.ENDPOINT, {
        method: 'post',
        body: data,
      });

      // const result = await response.json();
      // console.log('result', result);
      // const { setOpenPoseResult } = this.props;
      // setOpenPoseResult(result);
    } catch (e) {
      console.error(e);
    }
  }

  startRecording = async () => {
    this.setState({ recording: true });
    // default to mp4 for android as codec is not set
    const { uri, codec = 'H264' } = await this.camera.recordAsync();
   
    const savedUri = this.saveVideoToCameraRoll(uri);

    // this.sendVideoAndConfigToServer(savedUri, codec)
    this.setState({ recording: false });
  }

  stopRecording = () => {
    this.camera.stopRecording();
  }

  render() {
    const { recording } = this.state;

    return (
      <>
        <RNCamera
          ref={(ref) => {
            this.camera = ref;
          }}
          style={styles.preview}
          type={RNCamera.Constants.Type.back}
          flashMode={RNCamera.Constants.FlashMode.on}
        />
        <View
          style={styles.recordButtonContainer}
        >
          {
            <View style={styles.horizontalButtonContainer}>
              <TouchableOpacity
                onPress={recording ? this.stopRecording : this.startRecording}
                style={styles.recordButton}
              >
                <Text style={styles.recordButtonText}>
                  {recording ? 'STOP' : 'RECORD'}
                </Text>
              </TouchableOpacity>
              <TouchableOpacity
                onPress={this.selectVideo}
                style={styles.recordButton}
              >
                <Text style={styles.recordButtonText}>
                  Select
                </Text>
              </TouchableOpacity>
            </View>
          }
        </View>
      </>
    );
  }
}

CameraView.propTypes = {
  setOpenPoseResult: PropTypes.func.isRequired,
};

export default CameraView;
