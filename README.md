# ProudAuth organization profile

`profile/README.md` is the page at [github.com/ProudAuth](https://github.com/ProudAuth).

`assets/` holds the brand kit used across the organization: a README banner
and a social preview image for every repository, and the organization avatar.
`brand/make_brand.py` regenerates them from code (needs `rsvg-convert`):

```sh
python3 brand/make_brand.py out && mv out/*.png assets/ && mv out/*.svg brand/source/
```

Social previews are uploaded per repository in Settings → General → Social
preview; the avatar in the organization's Settings → Profile.
