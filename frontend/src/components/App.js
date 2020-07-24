import React, {Component} from 'react';
import {render} from "react-dom";

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            data: [],
            loaded: false,
            placeholder: "Loading"
        };
    }

    componentDidMount() {
        fetch("memo/").then(response => {
            if(response.status > 400) {
                return this.setState(() => {
                    return {
                        placeholder: "Something wrongs!"
                    };
                });
            }
            return response.json();
        }).then(data => {
            this.setState(() => {
                return {
                    data,
                    loaded: true
                };
            });
        });
    }

    render() {
        return (
            <ul>
                {
                    this.state.data.map(memo => {
                        return (
                            <li key={memo.id}>
                               <h1>{memo.title}</h1>
                                <h4>{memo.author}</h4>
                                <p>
                                    {memo.content}
                                </p>
                            </li>
                        );
                    })
                }
            </ul>
        );
    }
}

export default App;
const container = document.getElementById("app");
render(<App />, container);
