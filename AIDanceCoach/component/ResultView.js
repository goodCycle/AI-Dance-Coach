import React, { Component } from 'react';
import PropTypes from 'prop-types';
import {
  StyleSheet,
  View,
  Text,
  TouchableOpacity,
  Dimensions,
} from 'react-native';
import Video from 'react-native-video'; // For showing result video

const { width: windowWidth } = Dimensions.get('window');

const styles = StyleSheet.create({
  container: {
    flex: 1,
    flexDirection: 'column',
  },
  preview: {
    flex: 1,
    backgroundColor: 'gray',
    justifyContent: 'center',
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
  sampleVideoContainer: {
    // flex: 1,
  },
  trainVideoContainer: {
    // flex: 1,
  },
});

class ResultView extends Component {
  constructor(props) {
    super(props);
    this.state = {
      videoHeight: 0,
    };
  }

  render() {
    const { resultVideoPath, flushOpenPoseResult } = this.props;
    const sampleVideoUri = `${resultVideoPath}/media/temp_vid/sample.mp4`;
    const trialVideoUri = `${resultVideoPath}/media/temp_vid/trial.mp4`;

    const { videoHeight } = this.state;
    const videoSizeStyle = { width: windowWidth, height: videoHeight };

    return (
      <View style={styles.container}>
        <View style={styles.preview}>
          <View style={styles.sampleVideoContainer}>
            <Video
              source={{ uri: sampleVideoUri }}
              style={videoSizeStyle}
              repeat
              onLoad={({ naturalSize: { height, width } }) => {
                const ratio = height / width;
                this.setState({ videoHeight: windowWidth * ratio });
              }}
            />
          </View>
          <View style={styles.trainVideoContainer}>
            <Video
              source={{ uri: trialVideoUri }}
              style={videoSizeStyle}
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
