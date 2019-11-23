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
import Config from 'react-native-config';

import HeaderContainer from './HeaderContainer';

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
});

class CameraView extends Component {
  constructor() {
    super();
    this.state = this.getInitialState();
  }

  getInitialState() {
    return {
      recording: false,
      processing: false,
      result: null,
    };
  }

  startRecording = async () => {
    this.setState({ recording: true });
    // default to mp4 for android as codec is not set
    const { uri, codec = 'H264' } = await this.camera.recordAsync();
    this.setState({ recording: false, processing: true });
    const type = `video/${codec}`;

    const data = new FormData();
    data.append('file', {
      name: 'app-video',
      type,
      uri,
    });

    try {
      const response = await fetch(Config.ENDPOINT, {
        method: 'post',
        body: data,
      });
      const result = await response.json();
      this.setState({ result });
    } catch (e) {
      console.error(e);
    }

    this.setState({ processing: false });
  }

  stopRecording = () => {
    this.camera.stopRecording();
  }

  render() {
    const { recording, processing } = this.state;
    const { onPressStopRecord } = this.props;

    return (
      <View style={styles.container}>
        <HeaderContainer
          leftIcon="chevron-left"
          onPressLeftIcon={onPressStopRecord}
          headerText="Record Dance"
        />
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
          processing
            ? (
              <View style={styles.recordButton}>
                <ActivityIndicator animating size={18} />
              </View>
            )
            : (
              <TouchableOpacity
                onPress={recording ? this.stopRecording : this.startRecording}
                style={styles.recordButton}
              >
                <Text style={styles.recordButtonText}>
                  {recording ? 'STOP' : 'RECORD'}
                </Text>
              </TouchableOpacity>
            )
        }
        </View>
      </View>
    );
  }
}

CameraView.propTypes = {
  onPressStopRecord: PropTypes.func.isRequired,
};

export default CameraView;
