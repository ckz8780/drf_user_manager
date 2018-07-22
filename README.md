# DRF User Manager

Provides the ability to add/update/delete users via a Django REST API. No listing capabilities are allowed. This is a "write only" API.

## Tests implemented:

#### Setup:

	- setup
	- test_setup_created_correct_test_users

#### User Creation:

	- test_can_create_user_anonymously

#### User Updates:

	- test_cannot_update_user_anonymously
	- test_regular_user_cannot_update_other_users_info
	- test_user_can_update_own_info
	- test_admin_user_can_update_regular_users_info

#### User Deletions:

	- test_cannot_delete_user_anonymously
	- test_regular_user_cannot_delete_other_user
	- test_user_cannot_delete_self
	- test_admin_user_can_delete_regular_user

#### API Responses/Security:

	- test_api_response_to_user_creation_matches_post_data
	- test_password_not_in_create_user_api_response
	- test_password_not_in_update_user_api_response
	- test_password_not_in_delete_user_api_response
