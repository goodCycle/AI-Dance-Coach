import React, { Component } from 'react';
import PropTypes from 'prop-types';
import {
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
  Button,
  ActivityIndicator,
} from 'react-native';
import { RNCamera } from 'react-native-camera';
import Config from "react-native-config";

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
  capture: {
    backgroundColor: '#B82303',
    borderRadius: 5,
    color: '#000',
    padding: 10,
    marginHorizontal: 70,
    marginBottom: 10,
    alignItems: 'center',
    justifyContent: 'center',
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
    };
  }

  startRecording = async () => {
    this.setState({ recording: true });
    // default to mp4 for android as codec is not set
    const { uri, codec='H264' } = await this.camera.recordAsync();
    this.setState({ recording: false, processing: true });
    const type = `video/${codec}`;

    const data = new FormData();
    data.append('file', {
      name: 'app-video',
      type,
      uri
    });

    try {
      await fetch(Config.ENDPOINT, {
        method: "post",
        body: data
      })
      .then((response) => {
        console.log('response!', response.json());
      })
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

    let button = (
      <TouchableOpacity
        onPress={this.startRecording}
        style={styles.capture}
      >
        <Text style={{ fontSize: 14, color: '#fff' }}> RECORD </Text>
      </TouchableOpacity>
    );

    if (recording) {
      button = (
        <TouchableOpacity
          onPress={this.stopRecording}
          style={styles.capture}
        >
          <Text style={{ fontSize: 14 }}> STOP </Text>
        </TouchableOpacity>
      );
    }

    if (processing) {
      button = (
        <View style={styles.capture}>
          <ActivityIndicator animating size={18} />
        </View>
      );
    }

    const { onPressStopRecord } = this.props;

    return (
      <View style={styles.container}>
        <RNCamera
          ref={(ref) => {
            this.camera = ref;
          }}
          style={styles.preview}
          type={RNCamera.Constants.Type.back}
          flashMode={RNCamera.Constants.FlashMode.on}
        />
        <View
          style={{ flex: 0.3, flexDirection: 'column', justifyContent: 'center' }}
        >
          {button}
          <Button
            title="Go to Home"
            buttonStyle={{ backgroundColor: '#B82303' }}
            onPress={onPressStopRecord}
          />
        </View>
      </View>
    );
  }
}

CameraView.propTypes = {
  onPressStopRecord: PropTypes.func.isRequired,
};

export default CameraView;
