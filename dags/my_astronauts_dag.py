"""
## Print the number of people currently in space
"""

from airflow import Dataset
from airflow.models.dag import dag
from airflow.operators.bash import BashOperator
from airflow.operators.python import task
from pendulum import datetime


@dag(
    dag_id="my_astronaut_dag",
    start_date=datetime(2024, 1, 1),
    schedule=[Dataset("current_astronauts")],
    catchup=False,
    doc_md=__doc__,
    default_args={"ownder": "Astro", "retries": 3},
    tags=["My first DAG!"],
)
def my_astronaut_dag():
    @task
    def print_num_people_in_space(**context) -> None:
        """
        This task pulls the number of people currently in space from XCom. The number is
        pushed by the `get_astronauts` task in teh `example_astronauts` DAG.
        """

        num_people_in_space = context["ti"].xcom_pull(
            dag_id="example_astronauts",
            task_ids="get_astronauts",
            key="number_of_people_in_space",
            include_prior_dates=True,
        )

        print(f"There are currently {num_people_in_space} people in space.")


    print_reaction = BashOperator(
        task_id="print_reaction",
        bash_command="echo This is awesome!",
    )

    print_num_people_in_space() >> print_reaction

my_astronaut_dag()
