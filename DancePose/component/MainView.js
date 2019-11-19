'use strict';
import React, { Component } from 'react';
import {
  SafeAreaView,
  StyleSheet,
  ScrollView,
  View,
  Text,
  StatusBar,
  Container,
} from 'react-native';

import { Colors } from 'react-native/Libraries/NewAppScreen';

import { 
  Header,
  Button,
 } from 'react-native-elements';

import Icon from 'react-native-vector-icons/Entypo';
Icon.loadFont();

class MainView extends Component {
  render() {
    return (
      <>
        <Header
          containerStyle={{
            backgroundColor: '#B82303',
            justifyContent: 'space-around',
          }}
          leftComponent={<Icon name='menu' color='#fff' size={30} />}
          centerComponent={{ text: 'AI Dance Coach', style: { color: '#fff', fontSize: 20, fontWeight: 'bold' } }}
          rightComponent={<Icon name='home' color='#fff' size={30}/>}
        />
        <StatusBar barStyle="dark-content" />
        <SafeAreaView>
          <ScrollView
            contentInsetAdjustmentBehavior="automatic"
            style={styles.scrollView}>
            {global.HermesInternal == null ? null : (
              <View style={styles.engine}>
                <Text style={styles.footer}>Engine: Hermes</Text>
              </View>
            )}
            <View style={styles.body}>
              <View style={styles.sectionContainer}>
                <Text style={styles.sectionTitle}>Deep-learning based App</Text>
                <Text style={styles.sectionDescription}>
                  Apply Single-Network Whole-Body Pose Estimation which is based on <Text style={styles.highlight}>OpenPose</Text> library.
                </Text>
              </View>
              <View style={styles.sectionContainer}>
                <Text style={styles.sectionTitle}>Dancing Pose Correction</Text>
                <Text style={styles.sectionDescription}>
                  You can correct your dance by comparing your dancing with professional dancers.
                </Text>
              </View>
              <View style={styles.sectionContainer}>
                <Text style={styles.sectionTitle}>Easy to Use</Text>
                <Text style={styles.sectionDescription}>
                  Just record your dancing and press <Text style={styles.highlight}>Start Analysis</Text> button.
                </Text>
              </View>
              <View style={styles.sectionContainer}>
                <Text style={styles.sectionTitle}>Provide Feedback</Text>
                <Text style={styles.sectionDescription}>
                  You can get feedback of your dance pose which is compared with professional dancers.
                </Text>
              </View>
              <View style={{
                flex: 1,
                marginTop: 40,
                marginHorizontal: 64,
              }}>
                <Button
                  title='Start Record'
                  // titleStyle={{ fontWeight: 'bold' }}
                  buttonStyle= {{ backgroundColor: '#B82303' }}
                  onPress={() => {
                
                  }}
                />
              </View>
            </View>
          </ScrollView>
        </SafeAreaView>
      </>
    );
  }
}

const styles = StyleSheet.create({
  scrollView: {
    backgroundColor: Colors.lighter,
  },
  engine: {
    position: 'absolute',
    right: 0,
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
  footer: {
    color: Colors.dark,
    fontSize: 12,
    fontWeight: '600',
    padding: 4,
    paddingRight: 12,
    textAlign: 'right',
  },
});

export default MainView;