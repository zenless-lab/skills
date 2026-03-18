# BAD: Explaining "What" (redundant)
users = get_users()  # Get all users
for user in users:   # Loop through users
    user.activate()  # Activate the user

# GOOD: Explaining "Why"
# We must process users in batches of 50 to avoid hitting the
# rate limit on the external activation API.
for batch in get_user_batches(size=50):
    activate_users(batch)

# BAD: Hiding bad code with comments
# Check if u is active and has a valid subscription
if u.a and u.s > 0:
    process(u)

# GOOD: Refactoring instead of commenting
is_active_subscriber = user.is_active and user.subscription_days_left > 0
if is_active_subscriber:
    process(user)

# GOOD: Block comment with multiple paragraphs
# The following algorithm implements a custom retry logic for the database connection.
#
# We cannot use the standard tenacity library here because the database driver
# requires a specific teardown sequence on failure before reconnecting.
def connect_to_db():
    pass

# GOOD: Inline comment for obscure math
result = val * 0.986  # 0.986 is the empirically derived friction coefficient for the motor

# GOOD: Special markers
# FIXME: This nested loop is O(N^2) and will bottleneck when the list exceeds 10k items.
def calculate_distances(points):
    pass
