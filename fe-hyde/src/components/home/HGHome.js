import React from 'react';
import clsx from 'clsx';
import { withTheme, withStyles } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import Close from '@material-ui/icons/Close';
import MenuItem from '@material-ui/core/MenuItem';
import Menu from '@material-ui/core/Menu';
import AccountCircle from '@material-ui/icons/AccountCircle';
import HGDrawer from '../drawer/HGDrawer';
import Grid from '@material-ui/core/Grid';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import Container from '@material-ui/core/Container';
import HGContainer from '../container/HGContainer';

const drawerWidth = 240;

const styles = theme => ({
  root: {
    display: 'flex',
  },
  appBar: {
    transition: theme.transitions.create(['margin', 'width'], {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
  },
  appBarShift: {
    width: `calc(100% - ${drawerWidth}px)`,
    marginLeft: drawerWidth,
    transition: theme.transitions.create(['margin', 'width'], {
      easing: theme.transitions.easing.easeOut,
      duration: theme.transitions.duration.enteringScreen,
    }),
  },
  menuButton: {
    marginRight: theme.spacing(2),
  },
  hide: {
    display: 'none',
  },

  title: {
    flexGrow: 1,
  },

  content: {
    flexGrow: 1,
    padding: theme.spacing(3),
    transition: theme.transitions.create('margin', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
    marginLeft: -drawerWidth,
  },

  contentShift: {
    transition: theme.transitions.create('margin', {
      easing: theme.transitions.easing.easeOut,
      duration: theme.transitions.duration.enteringScreen,
    }),
    marginLeft: 0,
  },
});

class Home extends React.Component {

  constructor(props) {
    super(props)
    this.state = {
      // classes: useStyles(),
      // theme: useTheme(),
      openDrawer: false,
      anchorEl: null,
      auth: true,
      activeTabs: [],
      value: false,
      checked: false,
    }
    this.handleDrawerOpen = this.handleDrawerOpen.bind(this);
    this.handleDrawerClose = this.handleDrawerClose.bind(this);
    this.handleMenu = this.handleMenu.bind(this);
    this.handleClose = this.handleClose.bind(this);
    this.handleOpenRow = this.handleOpenRow.bind(this);
    this.handleChange = this.handleChange.bind(this);

  }

  handleDrawerOpen() {
    this.setState({ openDrawer: true });
  }

  handleDrawerClose() {
    this.setState({ openDrawer: false });
  }

  handleMenu(event) {
    this.setState({ anchorEl: event.currentTarget });
  }

  handleClose() {
    this.setState({ anchorEl: null });
  }

  handleOpenRow(row) {
    this.setState(state => {
      const activeTabs = state.activeTabs.concat(row);
      return { activeTabs };
    })
  }

  handleChange(event, newValue) {
    this.setState({ value: newValue });
  }

  render() {
    const open = Boolean(this.state.anchorEl);
    const { openDrawer } = this.state;
    const { classes } = this.props;
    const { auth, anchorEl } = this.state
    const { handleMenu, handleClose } = this;
    return (
      <div className={classes.root}>
        <CssBaseline />
        <AppBar
          position="fixed"
          className={clsx(classes.appBar, {
            [classes.appBarShift]: openDrawer,
          })}
        >
          <Grid container spacing={3}>
            <Grid item xs={2}>
              <Toolbar variant="dense">
                <IconButton
                  color="inherit"
                  aria-label="Open drawer"
                  onClick={this.handleDrawerOpen}
                  edge="start"
                  className={clsx(classes.menuButton, openDrawer && classes.hide)}
                >
                  <MenuIcon />
                </IconButton>
                <Typography variant="h6" className={classes.title}>
                  Gkeyll
                </Typography>
              </Toolbar>
            </Grid>
            <Grid item xs={9}>
              <Tabs value={this.state.value} onChange={this.handleChange} variant="scrollable"
                scrollButtons="auto">
                {this.state.activeTabs.map(tab => {
                  const node = (<div>{tab.name}<IconButton size="small"><Close /></IconButton></div>)
                  return (
                    <Tab label={node} key={tab.id} />
                  )
                })
                }
              </Tabs>
            </Grid>
            <Grid item xs={1}>
              {auth && (
                <div>
                  <IconButton
                    aria-label="Account of current user"
                    aria-controls="menu-appbar"
                    aria-haspopup="true"
                    onClick={handleMenu}
                    color="inherit">
                    <AccountCircle />
                  </IconButton>
                  <Menu
                    id="menu-appbar"
                    anchorEl={anchorEl}
                    anchorOrigin={{
                      vertical: 'top',
                      horizontal: 'right',
                    }}
                    keepMounted
                    transformOrigin={{
                      vertical: 'top',
                      horizontal: 'right',
                    }}
                    open={open}
                    onClose={handleClose}
                  >
                    <MenuItem onClick={handleClose}>Profile</MenuItem>
                    <MenuItem onClick={handleClose}>My account</MenuItem>
                  </Menu>
                </div>
              )}
            </Grid>
          </Grid>
        </AppBar>
        <HGDrawer open={openDrawer} onClickClose={this.handleDrawerClose}
          onClickOpenRow={this.handleOpenRow} />
        <main className={clsx(classes.content, {
          [classes.contentShift]: openDrawer,
        })}>
          <div className={classes.drawerHeader} />
          <Container maxWidth="xl">
            {this.state.activeTabs.map((tab, index) => (
              this.state.value === index &&
              <HGContainer />
            ))}
          </Container>
        </main>
      </div>
    );

  }
}

export default withTheme(withStyles(styles)(Home));