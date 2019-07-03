import React from 'react';
import EditorRunForm from '../editor/HGEditorRunForm';
import Switch from '@material-ui/core/Switch';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Typography from '@material-ui/core/Typography';


function TabContainer(props) {
    return (
        <Typography component="div" style={{ padding: 8 * 3 }}>
            {props.children}
        </Typography>
    );
}

class HGContainer extends React.Component {

    constructor(props) {
        super(props)
        this.state = {
            checked: false,
        }
        this.handleChange = this.handleChange.bind(this);
    }

    handleChange(event, newCheckedValue) {
        this.setState({ checked: newCheckedValue });
    }

    render() {
        return (
            <TabContainer>
                <FormControlLabel
                    control={
                        <Switch
                            checked={this.state.checked}
                            onChange={this.handleChange}
                            color="primary"
                        />
                    }
                    label="viz"
                />
                {!this.state.checked && <EditorRunForm />}
                {this.state.checked && <div> Visualization </div> }
            </TabContainer>
        );
    }
}
export default HGContainer;