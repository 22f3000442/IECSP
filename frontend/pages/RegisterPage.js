export default {
    template : `
    <div>
        <input placeholder="username"  v-model="username"/>
        <input placeholder="email"  v-model="email"/>
        <input placeholder="role"  v-model="role"/>  
        <input placeholder="password"  v-model="password"/>  
        <button  class='btn btn-warning' @click="submitLogin"> Register </button>
    </div>
    `,
    data(){
        return {
            username : null,
            password : null,
            email : null,
            role : null,
        } 
    },
    methods : {
        async submitLogin(){
            const res = await fetch(location.origin+'/register',
             {
                 method : 'POST',
                 headers: {'Content-Type' : 'application/json'}, 
                 body : JSON.stringify({'username': this.username,'password': this.password, 'email': this.email, 'role': this.role})
                })
            if (res.ok){
                console.log('we are registered')
                const data = await res.json()
                console.log(data)
            }
        }
    }
}