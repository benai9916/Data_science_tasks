from nanos import get_client_details, list_all_campaigns, get_campaign_details, render_tax_invoice
import stripe

''' Assuming that API response is not "hash" '''

################# TASK -1 #################
def get_unique_client_ids():
    campaign_ids = list_all_campaigns()
    client_ids = {}
    for campaign_id in campaign_ids:
        campaign_details = get_campaign_details(campaign_id)
        client_id = campaign_details['client_id']
        if not client_ids.get(client_id):
            client_ids[client_id] = True
    return list(client_ids.keys())


def create_tax_object(stripe_customer_id, vat_type, vat_number):
    stripe.Customer.create_tax_id(
        stripe_customer_id,
        type=vat_type,
        value=vat_number,
    )

def process_non_swiss_customers(client_details):
    try:
        stripe_customer_details = stripe.Customer.retrieve(client_details['stripe_customer_id'])

        if stripe_customer_details['tax_exempt'] != "exempt":
            stripe.Customer.modify(
                client_details['stripe_customer_id'],
                metadata={"tax_exempt": "exempt"},
            )
        return True
    except:
        return False

def process_swiss_customers(client_details):
    try:
        stripe_customer_details = stripe.Customer.retrieve(client_details['stripe_customer_id'])

        if stripe_customer_details['tax_exempt'] != "none":
            stripe.Customer.modify(
                client_details['stripe_customer_id'],
                metadata={"tax_exempt": "none"},
            )

        if client_details['vat_number']:
            client_tax_object = create_tax_object(client_details['stripe_customer_id'], "ch_vat", client_details['vat_number'])
        return True
    except:
        return False


def update_stripe_customer_info():
    # we are assuming from the task details that the stripe_customer_id always exists
    unique_client_ids = get_unique_client_ids()
    failed_client_ids = []
    updated_client_ids = []
    for client_id in unique_client_ids:
        client_details = get_client_details(client_id)

        if client_details['country'] == 'swiss':
            status = process_swiss_customers(client_details)
        else:
            status = process_non_swiss_customers(client_details)

        if status == 'failed':
            failed_client_ids.append(client_id)
        else:
            updated_client_ids.append(client_id)


################# TASK-2 #################
def generate_invoice(ad_campaign_id):
    campaign_details = get_campaign_details(ad_campaign_id)
    client_details = get_client_details(campaign_details['client_id'])

    # customer_details = stripe.Customer.retrieve(client_details['stripe_customer_id'])
    # charge_details = stripe.Charge.retrieve(campaign_details['stripe_charge_id'])
    charge_customer_invoice_details = stripe.Charge.retrieve(
        client_details['stripe_charge_id'],
        expand=['invoice']
    )

    render_tax_invoice(
        client_name = charge_customer_invoice_details['invoice']['customer_name'],
        client_email = charge_customer_invoice_details['invoice']['customer_email'],
        client_address = charge_customer_invoice_details['invoice']['customer_address'],
        campaign_name = campaign_details['name'],
        invoice_currency = charge_customer_invoice_details['invoice']['currency'],
        invoice_amount = charge_customer_invoice_details['invoice']['total'],
        vat_amount = charge_customer_invoice_details['invoice']['total_tax_amounts'],
        net_amount = (charge_customer_invoice_details['invoice']['total'] - charge_customer_invoice_details['invoice']['total_tax_amounts'])
    )
