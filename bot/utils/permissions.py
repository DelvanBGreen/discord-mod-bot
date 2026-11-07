ADMIN_ROLE_ID = 1568486132084248691 #REPLACE WITH YOUR ROLE ID
MOD_ROLE_ID = 0 


def is_admin(member):
    return any(role.id == ADMIN_ROLE_ID for role in member.roles)

def is_moderator(member):
    return any(role.id in (ADMIN_ROLE_ID, MOD_ROLE_ID)
               for role in member.roles)