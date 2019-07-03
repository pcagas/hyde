import React from "react";
import AceEditor from "react-ace";
import Button from '@material-ui/core/Button';

import "brace/mode/lua";
import "brace/theme/monokai";

export default class EditorRunForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            value: this.props.fileContent
        };

        this.handleChange = this.handleChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleChange(data) {
        // console.log(data);
        this.setState({ value: data });
        // this.setState({ value: this.props.fileContent });
    }

    handleSubmit(event) {
        event.preventDefault();
        fetch("/jobs/create", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 'filename': 'file/two-stream.lua' }),
        })
            .then(res => res.json())
            .then(
                (result) => {
                    alert("job submitted. id is " + result.id);
                    this.props.onJobSubmitted && this.props.onJobSubmitted(result.id);
                },
                (error) => {
                    console.log(error);
                }
            );
    }

    componentWillReceiveProps(nextProps) {
        if (nextProps.fileContent !== this.state.value) {
            this.setState({ value: nextProps.fileContent });
        }
    }

    render() {
        
        return (<form onSubmit={this.handleSubmit}>
            <AceEditor
                mode="lua"
                theme="monokai"
                fontSize={16}
                onChange={this.handleChange}
                name="hg_editor"
                showPrintMargin={true}
                showGutter={true}
                highlightActiveLine={true}
                value={this.state.value}
                editorProps={{ $blockScrolling: true }}
            />
            <Button variant="contained" color="primary">
                Submit
            </Button>
        </form>);
        // }
    }

}
