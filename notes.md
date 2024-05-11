## Todo:

- Want to be able to mount a `data` directory for local development
    - Maybe alter the `Dockerfile`?
    - Would have to enable astro's airflow docker user to modify host machine files
        - Easiest way to do this is to make airflow's `uid` the same as the host
        - Host uid is 1000
            - Setting `ASTRONOMER_UID=1000` in `.env`
            - `printenv` from within airflow docker container shows `ASTRONOMER_UID=1000`
            - `id -u` however show's the UID is still 50000 and permission denied 
                manipulating host files

