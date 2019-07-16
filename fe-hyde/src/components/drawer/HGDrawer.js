import React from 'react';
import { withTheme, withStyles } from '@material-ui/core/styles';
import SimList from '../sim/HGSimList';
import CreateFromNew from '../utilities//HGCreateFromNew';
import CreateFromExample from '../utilities/HGCreateFromExample';
import ChevronLeftIcon from '@material-ui/icons/ChevronLeft';
import ChevronRightIcon from '@material-ui/icons/ChevronRight';
import Divider from '@material-ui/core/Divider';
import Drawer from '@material-ui/core/Drawer';
import IconButton from '@material-ui/core/IconButton';

const drawerWidth = 240;

const styles = theme => ({

  drawer: {
    width: drawerWidth,
    flexShrink: 0,
  },
  drawerPaper: {
    width: drawerWidth,
  },
  drawerHeader: {
    display: 'flex',
    alignItems: 'center',
    padding: '0 8px',
    ...theme.mixins.toolbar,
    justifyContent: 'flex-end',
  },
  title: {
    flexGrow: 1,
  },

});

class HGDrawer extends React.Component {

  constructor(props) {
    super(props)
    this.handleDrawerClose = this.handleDrawerClose.bind(this);
    this.handleItemClick = this.handleItemClick.bind(this);
    
  }

  handleDrawerClose() {
    this.props.onClickClose && this.props.onClickClose();
  }

  handleItemClick(row){
    this.props.onClickOpenRow && this.props.onClickOpenRow(row);
  }

  render() {

    const { open } = this.props;
    const { classes, theme } = this.props;

    return (
      <Drawer
        className={classes.drawer}
        variant="persistent"
        anchor="left"
        open={open}
        classes={{
          paper: classes.drawerPaper,
        }}
      >
        <div className={classes.drawerHeader}>
          {/* <div className={classes.title}> */}
            <CreateFromNew onClickCreateFromNewButton={(row) => this.handleItemClick(row) } />
            <CreateFromExample onClickCreateFromExampleButton={(row) => this.handleItemClick(row) } />
          {/* </div> */}
          <IconButton onClick={this.handleDrawerClose}>
            {theme.direction === 'ltr' ? <ChevronLeftIcon /> : <ChevronRightIcon />}
          </IconButton>
        </div>
        <Divider />

        <SimList onClickItem={(row) => this.handleItemClick(row)}/>

      </Drawer>

    );
  }
}
export default withTheme(withStyles(styles)(HGDrawer));