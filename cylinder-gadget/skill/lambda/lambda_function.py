#
# The CylinderLight example use Amazon's ColorCycle structure as a basis (although only a limited piece of it remains).  That
# previous example was licensed as follows:
#
# Copyright 2019 Amazon.com, Inc. or its affiliates.  All Rights Reserved.
# These materials are licensed under the Amazon Software License in connection with the Alexa Gadgets Program.
# The Agreement is available at https://aws.amazon.com/asl/.
# See the Agreement for the specific terms and conditions of the Agreement.
# Capitalized terms not defined in this file have the meanings given to them in the Agreement.
# 
import logging.handlers
import requests
import uuid

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.serialize import DefaultSerializer
from ask_sdk_core.utils.request_util import get_slot_value

from ask_sdk_model import IntentRequest
from ask_sdk_model.ui import PlayBehavior

from ask_sdk_model.interfaces.custom_interface_controller import (
    StartEventHandlerDirective, EventFilter, Expiration, FilterMatchAction,
    StopEventHandlerDirective,
    SendDirectiveDirective,
    Header,
    Endpoint,
    EventsReceivedRequest,
    ExpiredRequest
)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
serializer = DefaultSerializer()
skill_builder = SkillBuilder()

@skill_builder.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input: HandlerInput):
    logger.info("== Launch Intent ==")

    response_builder = handler_input.response_builder

    system = handler_input.request_envelope.context.system
    api_access_token = system.api_access_token
    api_endpoint = system.api_endpoint

    # Get connected gadget endpoint ID.
    endpoints = get_connected_endpoints(api_endpoint, api_access_token)
    logger.debug("Checking endpoint..")
    if not endpoints:
        logger.debug("No connected gadget endpoints available.")
        return (response_builder
                .speak("No gadgets found. Please try again after connecting your gadget.")
                .set_should_end_session(True)
                .response)

    endpoint_id = endpoints[0]['endpointId']

    # Store endpoint ID for using it to send custom directives later.
    logger.debug("Received endpoints. Storing Endpoint Id: %s", endpoint_id)
    session_attr = handler_input.attributes_manager.session_attributes
    session_attr['endpointId'] = endpoint_id

    return (response_builder
            .speak("Hi! This is your cylinder light.  What would you like me to do?")
            .ask("Do you want to give me a command?")
            .set_should_end_session(False)
            .response)

@skill_builder.request_handler(can_handle_func=is_intent_name("AMAZON.FallbackIntent"))
def message_intent_handler(handler_input: HandlerInput):
    logger.info("Received FallbackIntent.")

    response_builder = handler_input.response_builder

    return (response_builder
            .speak("Sorry I didn't catch that.  What did you ask?")
            .set_should_end_session(False)
            .response)
            
@skill_builder.request_handler(can_handle_func=is_intent_name("MessageIntent"))
def message_intent_handler(handler_input: HandlerInput):
    logger.info("Received MessageIntent.")

    # Retrieve the stored gadget endpointId from the SessionAttributes.
    session_attr = handler_input.attributes_manager.session_attributes
    endpoint_id = session_attr['endpointId']

    response_builder = handler_input.response_builder
    message=get_slot_value(handler_input=handler_input,slot_name="Phrase")

    return (response_builder
            .speak("I will display "+message)
            .add_directive(build_cylinder_light_directive(endpoint_id,{"message":message}))
            .set_should_end_session(False)
            .response)
            
@skill_builder.request_handler(can_handle_func=is_intent_name("ForegroundColorIntent"))
def message_intent_handler(handler_input: HandlerInput):
    logger.info("Received ForcegroundColorIntent.")

    # Retrieve the stored gadget endpointId from the SessionAttributes.
    session_attr = handler_input.attributes_manager.session_attributes
    endpoint_id = session_attr['endpointId']

    response_builder = handler_input.response_builder
    color=get_slot_value(handler_input=handler_input,slot_name="Color")
    
    return (response_builder
            .speak("I'll change the foreground color to "+color)
            .add_directive(build_cylinder_light_directive(endpoint_id,{"fcolor":color}))
            .set_should_end_session(False)
            .response)
            
@skill_builder.request_handler(can_handle_func=is_intent_name("BackgroundColorIntent"))
def message_intent_handler(handler_input: HandlerInput):
    logger.info("Received BackgroundColorIntent.")

    # Retrieve the stored gadget endpointId from the SessionAttributes.
    session_attr = handler_input.attributes_manager.session_attributes
    endpoint_id = session_attr['endpointId']

    response_builder = handler_input.response_builder
    color=get_slot_value(handler_input=handler_input,slot_name="Color")

    return (response_builder
            .speak("I'll change the background color to "+color)
            .add_directive(build_cylinder_light_directive(endpoint_id,{"bcolor":color}))
            .set_should_end_session(False)
            .response)
            
@skill_builder.request_handler(can_handle_func=is_intent_name("ClearIntent"))
def message_intent_handler(handler_input: HandlerInput):
    logger.info("Received ClearIntent.")

    # Retrieve the stored gadget endpointId from the SessionAttributes.
    session_attr = handler_input.attributes_manager.session_attributes
    endpoint_id = session_attr['endpointId']

    response_builder = handler_input.response_builder

    return (response_builder
            .speak("Clearing the message.")
            .add_directive(build_cylinder_light_directive(endpoint_id,{"clear":"true"}))
            .set_should_end_session(False)
            .response)
            
@skill_builder.request_handler(can_handle_func=is_intent_name("NextIntent"))
def message_intent_handler(handler_input: HandlerInput):
    logger.info("Received NextIntent.")

    # Retrieve the stored gadget endpointId from the SessionAttributes.
    session_attr = handler_input.attributes_manager.session_attributes
    endpoint_id = session_attr['endpointId']

    response_builder = handler_input.response_builder

    return (response_builder
            .speak("Changing to the next mode.")
            .add_directive(build_cylinder_light_directive(endpoint_id,{"next":"true"}))
            .set_should_end_session(False)
            .response)
            
@skill_builder.request_handler(can_handle_func=lambda handler_input:
                               is_intent_name("AMAZON.CancelIntent")(handler_input) or
                               is_intent_name("AMAZON.StopIntent")(handler_input))
def stop_and_cancel_intent_handler(handler_input):
    logger.info("Received a Stop or a Cancel Intent..")
    session_attr = handler_input.attributes_manager.session_attributes
    response_builder = handler_input.response_builder
    endpoint_id = session_attr['endpointId']

    # When the user stops the skill, stop the EventHandler,
    if 'token' in session_attr.keys():
        logger.debug("Active session detected, sending stop EventHandlerDirective.")
        response_builder.add_directive(StopEventHandlerDirective(session_attr['token']))

    return (response_builder
            .speak("Alright, see you later.")
            .set_should_end_session(True)
            .response)


@skill_builder.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input):
    logger.info("Session ended with reason: " +
                handler_input.request_envelope.request.reason.to_str())
    return handler_input.response_builder.response


@skill_builder.exception_handler(can_handle_func=lambda i, e: True)
def error_handler(handler_input, exception):
    logger.info("==Error==")
    logger.error(exception, exc_info=True)
    return (handler_input.response_builder
            .speak("I'm sorry, something went wrong!").response)


@skill_builder.global_request_interceptor()
def log_request(handler_input):
    # Log the request for debugging purposes.
    logger.info("==Request==\r" +
                str(serializer.serialize(handler_input.request_envelope)))


@skill_builder.global_response_interceptor()
def log_response(handler_input, response):
    # Log the response for debugging purposes.
    logger.info("==Response==\r" + str(serializer.serialize(response)))
    logger.info("==Session Attributes==\r" +
                str(serializer.serialize(handler_input.attributes_manager.session_attributes)))


def get_connected_endpoints(api_endpoint, api_access_token):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(api_access_token)
    }

    api_url = api_endpoint + "/v1/endpoints"
    endpoints_response = requests.get(api_url, headers=headers)

    if endpoints_response.status_code == requests.codes['ok']:
        return endpoints_response.json()["endpoints"]

def build_cylinder_light_directive(endpoint_id, map):
    return SendDirectiveDirective(
        header=Header(namespace='Custom.CylinderLightGadget', name='Message'),
        endpoint=Endpoint(endpoint_id=endpoint_id),
        payload=map
    )

lambda_handler = skill_builder.lambda_handler()
