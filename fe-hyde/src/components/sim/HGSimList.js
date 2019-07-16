import React from 'react';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import FolderIcon from '@material-ui/icons/Folder';
import ListItemSecondaryAction from '@material-ui/core/ListItemSecondaryAction';

function createData(id, name, start, status) {
    return { id, name, start, status };
}

const rows = [
    createData('00001', 'sim1', 'today', 'completed'),
    createData('00002', 'sim2', 'today', 'running'),
    createData('00003', 'sim3', 'today', 'queued'),
    createData('00004', 'sim4', 'today', 'editing'),
    createData('00005', 'sim5', 'today', 'editing'),
];

class SimList extends React.Component {

    constructor(props) {
        super(props)
        this.state = {
            sims: [],
        }
        this.onSimRowClick = this.onSimRowClick.bind(this);
    }

    componentDidMount() {
        // fetch(`http://${location.hostname}:3000/api/sims`)
        fetch(`http://localhost:3000/api/sims`)
            .then(response => response.json())
            .then(data => this.setState({ sims: data.sims }));
    }

    onSimRowClick(row) {
        this.props.onClickItem && this.props.onClickItem(row);
    }

    render() {
        return (
            <List>
                {this.state.sims.map(row => (
                    <ListItem button key={row.id}
                        onClick={() => this.onSimRowClick(row)}
                    >
                        <ListItemIcon>
                            <FolderIcon />
                        </ListItemIcon>
                        <ListItemText
                            primary={row.name}
                        // secondary={row.inpFile}
                        />
                        <ListItemSecondaryAction>
                            {new Intl.DateTimeFormat('en-US').format(new Date(row.dateCreated))}
                        </ListItemSecondaryAction>
                    </ListItem>
                ))}
            </List>

        );
    }
}
export default SimList;