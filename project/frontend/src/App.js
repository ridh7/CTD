import React from 'react'
import Main from './Instruction/Main'
import {BrowserRouter, Route, Switch} from 'react-router-dom'
import AppCoding from './Coding/AppCoding'

class App extends React.Component {
    render() {
        return (
            <BrowserRouter>
                <div >
                    <Switch>
                        <Route exact path='/Coding' component={AppCoding} />
                        <Route path='/' component={Main} />
                    </Switch>
                </div>
            </BrowserRouter>
        )
    }

}

export default App