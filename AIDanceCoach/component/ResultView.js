import React, { Component } from 'react';
import PropTypes from 'prop-types';
import {
  StyleSheet,
  View,
  Text,
  TouchableOpacity,
} from 'react-native';

const styles = StyleSheet.create({
  container: {
    flex: 1,
    flexDirection: 'column',
  },
  preview: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  buttonContainer: {
    flex: 0.2,
    flexDirection: 'row',
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
      recording: false,
      processing: false,
      hasOpenPoseResult: false,
      openPoseResult: null,
    };
  }

  render() {
    const { openPoseResult, flushOpenPoseResult } = this.props;

    return (
      <View style={styles.container}>
        <View style={styles.preview}>
          <Text>{openPoseResult}</Text>
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
  openPoseResult: PropTypes.objectOf().isRequired,
  flushOpenPoseResult: PropTypes.func.isRequired,
};

export default ResultView;
