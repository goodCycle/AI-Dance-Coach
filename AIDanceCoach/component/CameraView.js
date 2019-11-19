'use strict';
import React, { Component } from 'react';
import PropTypes from 'prop-types';
import {
  AppRegistry,
  Dimensions,
  StyleSheet,
  Text,
  TouchableOpacity,
  View,
  Button
} from 'react-native';
import { RNCamera } from 'react-native-camera';
// import Config from "react-native-config";

class CameraView extends Component {
  constructor() {
    super();
    this.state = this.getInitialState();
  }

  getInitialState() {
    return {
      recording: false,
      processing: false
    };
  }

  render() {
    const { recording, processing } = this.state;

    let button = (
      <TouchableOpacity
        onPress={this.startRecording.bind(this)}
        style={styles.capture}
      >
        <Text style={{ fontSize: 14 }}> RECORD </Text>
      </TouchableOpacity>
    );

    if (recording) {
      button = (
        <TouchableOpacity
          onPress={this.stopRecording.bind(this)}
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

    return (
      <View style={styles.container}>
        <RNCamera
          ref={ref => {
            this.camera = ref;
          }}
          style={styles.preview}
          type={RNCamera.Constants.Type.back}
          flashMode={RNCamera.Constants.FlashMode.on}
        />
        <View
          style={{ flex: 1, flexDirection: "column", justifyContent: "center" }}
        >
          {button}
          <Button
            title='Stop Record'
            // titleStyle={{ fontWeight: 'bold' }}
            buttonStyle= {{ backgroundColor: '#B82303' }}
            onPress={this.props.onPressStopRecord}
          />
        </View>
      </View>
    );
  }

  async startRecording() {
    this.setState({ recording: true });
    // default to mp4 for android as codec is not set
    const { uri, codec = "mp4" } = await this.camera.recordAsync();
    this.setState({ recording: false, processing: true });
    const type = `video/${codec}`;
  
    const data = new FormData();
    data.append("video", {
      name: "mobile-video-upload",
      type,
      uri
    });
  
    try {
      // await fetch(Config.ENDPOINT, {
      //   method: "post",
      //   body: data
      // });
      console.log('fetch!');
    } catch (e) {
      console.error(e);
    }
  
    this.setState({ processing: false });
  }

  stopRecording() {
      this.camera.stopRecording();
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    flexDirection: 'row',
  },
  preview: {
    flex: 1,
    justifyContent: 'flex-end',
    alignItems: 'center'
  },
  capture: {
    flex: 0,
    backgroundColor: '#fff',
    borderRadius: 5,
    color: '#000',
    padding: 10,
    margin: 40
  }
});

CameraView.propTypes = {
  onPressStopRecord: PropTypes.func.isRequired,
};

export default CameraView;