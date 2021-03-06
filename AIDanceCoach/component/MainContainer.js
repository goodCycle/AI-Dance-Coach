import React, { Component } from 'react';
import PropTypes from 'prop-types';
import {
  StyleSheet,
  ScrollView,
  View,
  Text,
  TouchableOpacity,
} from 'react-native';

import { Colors } from 'react-native/Libraries/NewAppScreen';

import HeaderComponent from './HeaderComponent';

const styles = StyleSheet.create({
  scrollView: {
    backgroundColor: Colors.lighter,
    flex: 1,
  },
  srollViewContainerStyle: {
    flex: 1,
  },
  sectionContainer: {
    marginTop: 32,
    paddingHorizontal: 24,
    flex: 1,
  },
  sectionTitle: {
    fontSize: 24,
    fontWeight: '600',
    color: Colors.black,
  },
  sectionDescription: {
    marginTop: 8,
    fontSize: 18,
    fontWeight: '400',
    color: Colors.dark,
  },
  highlight: {
    fontWeight: '700',
  },
  buttonContainer: {
    marginTop: 40,
    marginBottom: 120,
    marginHorizontal: 70,
    justifyContent: 'center',
    flexDirection: 'row',
    backgroundColor: '#B82303',
  },
  buttonText: {
    color: '#fff',
    marginVertical: 10,
    fontSize: 18,
    fontWeight: 'bold',
  },
});

class MainContainer extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    const { onPressStartRecord } = this.props;

    return (
      <>
        <HeaderComponent
          leftIcon="menu"
          headerText="AI Dance Coach"
        />
        <ScrollView
          contentInsetAdjustmentBehavior="automatic"
          style={styles.scrollView}
          contentContainerStyle={styles.srollViewContainerStyle}
        >
          <View style={styles.sectionContainer}>
            <Text style={styles.sectionTitle}>Deep-learning based App</Text>
            <Text style={styles.sectionDescription}>
              Apply
              <Text style={styles.highlight}> OpenPose </Text>
              pose estimation deep learning library.
            </Text>
          </View>
          <View style={styles.sectionContainer}>
            <Text style={styles.sectionTitle}>Pose Correction</Text>
            <Text style={styles.sectionDescription}>
              You can correct your pose by comparing your dancing with professional dancers.
            </Text>
          </View>
          <TouchableOpacity
            style={styles.buttonContainer}
            onPress={onPressStartRecord}
          >
            <Text style={styles.buttonText}>Start Record</Text>
          </TouchableOpacity>
        </ScrollView>
      </>
    );
  }
}

MainContainer.propTypes = {
  onPressStartRecord: PropTypes.func.isRequired,
};

export default MainContainer;
