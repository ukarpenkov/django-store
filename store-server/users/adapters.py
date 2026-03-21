from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        if sociallogin.account.provider == "github" and getattr(
            user, "is_verified_email", False
        ) is False:
            if user.email:
                user.is_verified_email = True
                user.save(update_fields=["is_verified_email"])
        return user
