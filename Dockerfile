FROM python:3.12.7 AS compiler

WORKDIR /app/

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY ./requirements.txt /app/requirements.txt
RUN pip install -Ur requirements.txt

FROM python:3.12.7 AS runner

WORKDIR /app/ 
COPY --from=compiler /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY . /app/
EXPOSE 8000
CMD [ "python", "main.py" ]
