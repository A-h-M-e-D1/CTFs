# API-Mass Assignment

→ First check URL what is return 

![begin.png](API-Mass%20Assignment%2018247c97d4b3801d921efd19187d883e/begin.png)

This detect  the API endpoint and how it use so I try all this endpoint to understand this behavior.

##Singup → use to create new user

![signup.png](API-Mass%20Assignment%2018247c97d4b3801d921efd19187d883e/signup.png)

##Try Login

→ After login you can use

![used.png](API-Mass%20Assignment%2018247c97d4b3801d921efd19187d883e/used.png)

##Try this endpoints 

![get_info.png](API-Mass%20Assignment%2018247c97d4b3801d921efd19187d883e/get_info.png)

→ I think here if i can use way to change status into “admin” to the the flag as the guest user can’t read this 

![admin_auth_not.png](API-Mass%20Assignment%2018247c97d4b3801d921efd19187d883e/admin_auth_not.png)

→ First, I thought the endpoint /api/note could change note

![note_api.png](API-Mass%20Assignment%2018247c97d4b3801d921efd19187d883e/note_api.png)

→ the result after update

![after_update_note.png](API-Mass%20Assignment%2018247c97d4b3801d921efd19187d883e/after_update_note.png)

→ so I think if can change status in  this 

![first_try.png](API-Mass%20Assignment%2018247c97d4b3801d921efd19187d883e/first_try.png)

→ but it failed 

⇒ so Think if I modify in the /api/user/ itself so try this 

![think_1.png](API-Mass%20Assignment%2018247c97d4b3801d921efd19187d883e/think_1.png)

→ This detect it’s not change by this way so Think to modify HTTP request method into PUT

![think_2.png](API-Mass%20Assignment%2018247c97d4b3801d921efd19187d883e/think_2.png)

→ This Error is very useful and tell me that need Content-Type:application/json to change so Try it

![succees_change_status.png](API-Mass%20Assignment%2018247c97d4b3801d921efd19187d883e/succees_change_status.png)

→ Check the endpoint response again and will see the status code changed

![admin_status.png](API-Mass%20Assignment%2018247c97d4b3801d921efd19187d883e/admin_status.png)

→ Yes, it's changed successfully😁

---

→get the flag 😈

![flag_screen.png](API-Mass%20Assignment%2018247c97d4b3801d921efd19187d883e/flag_screen.png)

---

→ submit Flag 

![ok.png](API-Mass%20Assignment%2018247c97d4b3801d921efd19187d883e/ok.png)