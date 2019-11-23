import React, { Component } from 'react';
import PropTypes from 'prop-types';
import {
  StyleSheet,
  Text,
  TouchableOpacity,
} from 'react-native';
import {
  Header,
} from 'react-native-elements';

import Icon from 'react-native-vector-icons/Entypo';

const styles = StyleSheet.create({
  headerContainerStyle: {
    backgroundColor: '#B82303',
    justifyContent: 'space-around',
  },
  headerIconStyle: {
    color: '#fff',
    fontSize: 30,
  },
  headerTextStyle: {
    color: '#fff',
    fontSize: 20,
    fontWeight: 'bold',
  },
});

class HeaderContainer extends Component {
  constructor(props) {
    super(props);
    this.state = this.getInitialState();
  }

  getInitialState() {
    return {
    };
  }

  render() {
    const {
      leftIcon,
      onPressLeftIcon,
      headerText,
    } = this.props;

    return (
      <Header
        containerStyle={styles.headerContainerStyle}
        leftComponent={(
          <TouchableOpacity onPress={onPressLeftIcon}>
            <Icon name={leftIcon} style={styles.headerIconStyle} />
          </TouchableOpacity>
        )}
        centerComponent={<Text style={styles.headerTextStyle}>{headerText}</Text>}
      />
    );
  }
}

HeaderContainer.propTypes = {
  leftIcon: PropTypes.string.isRequired,
  onPressLeftIcon: PropTypes.func,
  headerText: PropTypes.string.isRequired,
};

HeaderContainer.defaultProps = {
  onPressLeftIcon: () => {},
};

export default HeaderContainer;
