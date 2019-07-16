import React from 'react';
import Tab from '@material-ui/core/Tab';
import IconButton from '@material-ui/core/IconButton';
import Close from '@material-ui/icons/Close';


class MyTab extends React.Component {

    constructor(props) {
        super(props)

        this.handleTabClose = this.handleTabClose.bind(this);
    }

    handleTabClose() {
        this.props.onTabClose && this.props.onTabClose(this.props.label);
    }

    render() {
        const { onTabClose, ...others } = this.props;
        return (
            <div>
                <Tab {...others} />
                <IconButton onClick={this.handleTabClose}><Close /></IconButton>
            </div>
        )
    }

}
export default MyTab;