/**
 * @format
 */

import 'react-native';
// Note: test renderer must be required after react-native.
import renderer from 'react-test-renderer';
import React from 'react';
import App from '../App';


it('renders correctly', () => {
  renderer.create(<App />);
});
