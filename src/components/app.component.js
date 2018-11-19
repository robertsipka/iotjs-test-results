/*
 * Copyright 2018 Samsung Electronics Co., Ltd. and other contributors
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import React from 'react';
import PropTypes from 'prop-types';
import { Switch, Route } from 'react-router';
import Header from './header/header.component';
import Footer from './footer/footer.component';
import Overview from './overview/overview.component';
import Device from './device/device.container';

export default class App extends React.Component {
  render() {
    const { match } = this.props;
    return (
      <div className="wrapper">
        <Header {...this.props} />

        <Switch>
          <Route exact path={match.path} component={Overview} />
          <Route path={`${match.path}/:device`} component={Device} />
        </Switch>

        <Footer />
      </div>
    );
  }
}

App.propTypes = {
  match: PropTypes.object.isRequired,
};
