import React, { Component } from 'react';
import PropTypes from 'prop-types';
import {
  SafeAreaView,
  StyleSheet,
  ScrollView,
  View,
  Text,
  StatusBar,
  TouchableOpacity,
} from 'react-native';

import { Colors } from 'react-native/Libraries/NewAppScreen';

import HeaderContainer from './HeaderContainer';

const styles = StyleSheet.create({
  scrollView: {
    backgroundColor: Colors.lighter,
  },
  body: {
    backgroundColor: Colors.white,
  },
  sectionContainer: {
    marginTop: 32,
    paddingHorizontal: 24,
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
    flex: 1,
    marginTop: 40,
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

class MainView extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    const { onPressStartRecord } = this.props;

    return (
      <>
        <HeaderContainer
          leftIcon="menu"
          headerText="AI Dance Coach"
        />
        <StatusBar barStyle="dark-content" />
        <SafeAreaView>
          <ScrollView
            contentInsetAdjustmentBehavior="automatic"
            style={styles.scrollView}
          >
            <View style={styles.body}>
              <View style={styles.sectionContainer}>
                <Text style={styles.sectionTitle}>Deep-learning based App</Text>
                <Text style={styles.sectionDescription}>
                  Apply Single-Network Whole-Body Pose Estimation which is based on
                  <Text style={styles.highlight}>OpenPose</Text>
                  library.
                </Text>
              </View>
              <View style={styles.sectionContainer}>
                <Text style={styles.sectionTitle}>Dancing Pose Correction</Text>
                <Text style={styles.sectionDescription}>
                  You can correct your dance by comparing your dancing with professional dancers.
                </Text>
              </View>
              <TouchableOpacity
                style={styles.buttonContainer}
                onPress={onPressStartRecord}
              >
                <Text style={styles.buttonText}>Start Record</Text>
              </TouchableOpacity>
            </View>
          </ScrollView>
        </SafeAreaView>
      </>
    );
  }
}

MainView.propTypes = {
  onPressStartRecord: PropTypes.func.isRequired,
};

export default MainView;
