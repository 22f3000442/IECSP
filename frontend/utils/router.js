const Home = {
    template : `<h1> this is my home </h1>`
}
import campaignListPage from "../pages/campaignListPage.js";
import LoginPage from "../pages/LoginPage.js";
import RegisterPage from "../pages/RegisterPage.js";
import campaignDisplayPage from "../pages/campaignDisplayPage.js";
import store from './store.js'
import adminDashboardPage from "../pages/adminDashboardPage.js";
import sponsorDashboardPage from "../pages/sponsorDashboardPage.js";

const routes = [
    {path : '/', component : Home},
    {path : '/login', component : LoginPage},
    {path : '/register', component : RegisterPage},
    {path : '/campaigns', component : campaignListPage, meta : {requiresLogin : true}},
    {path : '/campaigns/:id', component : campaignDisplayPage, props : true, meta : {requiresLogin : true}},
    {path : '/admin-dashboard', component : adminDashboardPage, props : true, meta : {requiresLogin : true, role : "admin"}},
    {path : '/sponsor-dashboard', component : sponsorDashboardPage, props : true, meta : {requiresLogin : true, role : "sponsor"}},
]

const router = new VueRouter({
    routes
})

router.beforeEach((to, from, next) => {
    if (to.matched.some((record) => record.meta.requiresLogin)){
        if (!store.state.loggedIn){
            next({path : '/login'});
        } else if (to.meta.role && to.meta.role !==store.state.role){
            alert('role not authorized')
            next({path : '/'});
        } else{
            next();
        }
    } else {
        next();
    }
})

export default router;