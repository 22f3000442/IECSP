import campaignCard from "../components/campaignCard.js"

export default {
    template : `
    <div class="p-4">
        <h1> Campaigns List </h1\>
        <campaignCard 
            v-for="campaign in campaigns"
            :key="campaign.id"
            :name = "campaign.name" 
            :start_date = "campaign.start_date" 
            :end_date = "campaign.end_date" 
            :sponsor_id = "campaign.sponsor_id" 
            :campaign_id="campaign.id"
        />
    </div>
    `,
    data(){
        return {
        campaigns : []
        }
    },
    methods : {

    },
    async mounted(){
        const res = await fetch(location.origin + '/api/campaigns',{
            headers : {
                'Authentication-Token' : this.$store.state.auth_token
            }
        })
        this.campaigns = await res.json()

    },
    components : {
        campaignCard,
    }

}