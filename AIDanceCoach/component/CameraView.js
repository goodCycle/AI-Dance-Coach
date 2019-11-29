import React, { Component } from 'react';
import PropTypes from 'prop-types';
import {
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
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
      mediaType: 'video',
    };

    ImagePicker.launchImageLibrary(options, (response) => {
      // Same code as in above section!
      console.log('SAVE!', response.uri);
      // const source = { uri: response.uri };
      // console.log('URI!!', source.uri);
      if (response.error) {
        console.log('ImagePicker Error: ', response.error);
      } else {
        this.sendVideoAndConfigToServer(response.uri);
      }
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
      compare_to: 'three_new.mp4',
    };
    const configJson = JSON.stringify(config);
    const configFileName = '/config.json';
    const jsonPath = RNFS.DocumentDirectoryPath + configFileName;

    // Write json to the file
    await RNFS.writeFile(jsonPath, configJson, 'utf8');

    data.append('file', {
      name: 'video_config.json',
      type: 'applpication/json',
      uri: jsonPath,
    });

    try {
      const response = await fetch(Config.SERVER_ENDPOINT, {
        method: 'post',
        body: data,
      });
      // TODO: save server response with zip
      console.log('server!!', response);
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
    const { uri } = await this.camera.recordAsync();

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
        </View>
      </>
    );
  }
}

CameraView.propTypes = {
  setOpenPoseResult: PropTypes.func.isRequired,
};

export default CameraView;
